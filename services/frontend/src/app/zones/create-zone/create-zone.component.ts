import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import {
  FileSystemDirectoryEntry,
  FileSystemFileEntry,
  NgxFileDropEntry,
} from 'ngx-file-drop';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { FileService } from 'src/app/files/file.service';
import { Location, LocationService } from 'src/app/locations/location.service';
import { Zone, ZonesService } from '../zones.service';

@Component({
  selector: 'app-create-zone',
  templateUrl: './create-zone.component.html',
  styleUrls: ['./create-zone.component.scss'],
})
export class CreateZoneComponent implements OnInit {
  zone: FormGroup;

  allLocations: Location[];
  errorMessage: string;

  //search location
  src: string = '';

  picture: FormGroup;
  url: string;
  public files: NgxFileDropEntry[] = [];

  @Input() fetchedCoordinates: any; // object {lat:  number, lng: number}
  @Output() close = new EventEmitter<void>();
  @Output() create = new EventEmitter<Zone>();

  constructor(
    private zoneService: ZonesService,
    private locationService: LocationService,
    private formBuilder: FormBuilder,
    private fileService: FileService
  ) {
    this.getLocations();
  }

  ngOnInit(): void {
    this.setZoneForm();
  }

  setZoneForm() {
    this.zone = new FormGroup({
      longitude: new FormControl(this.fetchedCoordinates.lng, [
        Validators.required,
        Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/),
      ]),
      latitude: new FormControl(this.fetchedCoordinates.lat, [
        Validators.required,
        Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/),
      ]),
      radius: new FormControl(null, [Validators.required, Validators.min(20),  Validators.max(2000)]),
      title: new FormControl('', [
        Validators.required,
        Validators.minLength(5),
        Validators.maxLength(200),
      ]),
      active: new FormControl(true, [Validators.required]),
      secret: new FormControl(false, [Validators.required]),
      location: new FormControl({}, [Validators.required]),
      description: new FormControl('', [Validators.maxLength(500)]),
      preview_image_filename: new FormControl(null),
      actual_address: new FormControl('', [Validators.required]),
    });

    this.picture = this.formBuilder.group({
      avatar: [],
    });
  }

  createZone() {
    let z = this.zone.value;
    let newZone: Zone = {
      title: z.title,
      latitude: z.latitude,
      longitude: z.longitude,
      radius: z.radius,
      location_id: z.location.id,
      active: z.active,
      secret: z.secret,
      description: z.description,
      actual_address: z.actualAddress,
    };
    if (z.preview_image_filename) {
      newZone.preview_image_filename = z.preview_image_filename;
    }

    this.zoneService.createZone(newZone).subscribe(
      (res) => {
        this.create.emit(res);
        this.close.emit();
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );

    this.zone.reset();
    this.src = '';
  }

  getLocations() {
    this.locationService.getLocations().subscribe(
      (res) => {
        //get user location id
        let userLocationId = +localStorage.getItem('user_location_id');

        //get all children locations for user location
        this.allLocations = this.locationService.getLocationChildren(
          res,
          userLocationId
        );

        //set parent name for all location
        this.allLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l);
          }
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }

  onFileChange(picture) {
    if (this.zone.get('preview_image_filename').value) {
      //if user wants to change picture, but one was picked, delete it from server
      this.fileService
        .deleteFile(this.zone.get('preview_image_filename').value)
        .subscribe(
          () => {},
          (error) => {
            this.errorMessage = error;
          }
        );
    }

    //upload new picture
    this.picture.get('avatar').setValue(picture);
    let formData = new FormData();
    formData.append('file', this.picture.get('avatar').value);

    this.fileService.postFile(formData).subscribe(
      (res) => {
        this.zone.get('preview_image_filename').setValue(res.filename);
        this.url = this.fileService.getFileByName(res.filename);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }

  public droppedPicture(files: NgxFileDropEntry[]) {
    this.files = files;
    for (const droppedFile of files) {
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          this.onFileChange(file);
        });
      } else {
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }
}
