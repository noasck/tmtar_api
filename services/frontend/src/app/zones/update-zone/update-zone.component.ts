import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import {
  FileSystemDirectoryEntry,
  FileSystemFileEntry,
  NgxFileDropEntry,
} from 'ngx-file-drop';
import { FileService } from 'src/app/files/file.service';
import { Location, LocationService } from 'src/app/locations/location.service';
import { Zone, ZonesService } from '../zones.service';

@Component({
  selector: 'app-update-zone',
  templateUrl: './update-zone.component.html',
  styleUrls: ['./update-zone.component.scss'],
})
export class UpdateZoneComponent implements OnInit {
  zone: FormGroup;

  allLocations: Location[];
  errorMessage: string;

  zoneLocation: Location;

  //search location
  src: string = '';

  picture: FormGroup;
  url: string;
  public files: NgxFileDropEntry[] = [];

  @Input() fetchedZone: Zone; //zone for update
  @Input() coordinates?: any; // object {lat:  number, lng: number}
  @Output() close = new EventEmitter<void>();
  @Output() update: EventEmitter<any> = new EventEmitter<void>();

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
    this.url = this.fetchedZone.preview_image_filename
      ? this.fileService.getFileByName(this.fetchedZone.preview_image_filename)
      : '';
  }

  setZoneForm() {
    this.zone = new FormGroup({
      longitude: new FormControl(
        this.coordinates ? this.coordinates.lng : this.fetchedZone.longitude,
        [Validators.required, Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/)]
      ),
      latitude: new FormControl(
        this.coordinates ? this.coordinates.lat : this.fetchedZone.latitude,
        [Validators.required, Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/)]
      ),
      radius: new FormControl(this.fetchedZone.radius, [
        Validators.required,
        Validators.min(20),
        Validators.max(2000),
      ]),
      title: new FormControl(this.fetchedZone.title, [
        Validators.required,
        Validators.minLength(5),
        Validators.maxLength(200),
      ]),
      active: new FormControl(this.fetchedZone.active),
      secret: new FormControl(this.fetchedZone.secret),
      location: new FormControl(this.zoneLocation),
      description: new FormControl(this.fetchedZone.description, [
        Validators.maxLength(500),
      ]),
      preview_image_filename: new FormControl(null),
      actual_address: new FormControl(this.fetchedZone.actual_address),
    });

    this.picture = this.formBuilder.group({
      avatar: [],
    });
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

        this.setZoneLocation(this.fetchedZone.location_id);
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  updateZone() {
    let formData = this.zone.value;
    let update: Zone = {
      title: formData.title,
      latitude: formData.latitude,
      longitude: formData.longitude,
      radius: formData.radius,
      location_id: formData.location
        ? formData.location.id
        : this.fetchedZone.location_id,
      active: formData.active,
      secret: formData.secret,
      description: formData.description,
      actual_address: formData.actualAddress,
    };

    if (formData.preview_image_filename) {
      update.preview_image_filename = formData.preview_image_filename;
    }
    this.zoneService.updateZone(this.fetchedZone.id, update).subscribe(
      (res) => {
        this.fetchedZone = res;
        this.update.emit(res);
      },
      (error) => {
        this.errorMessage = error;
      }
    );

    this.src = '';
    this.setZoneLocation(this.fetchedZone.location_id);
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }

  setZoneLocation(id) {
    this.zoneLocation = this.allLocations.filter(
      (location) => location.id == this.fetchedZone.location_id
    )[0];
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
