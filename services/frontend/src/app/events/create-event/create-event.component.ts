import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { FileService } from 'src/app/files/file.service';
import { Location, LocationService } from 'src/app/locations/location.service';
import { TransferService } from 'src/app/transfer.service';
import { Event, EventService } from '../events.service';
import {
  NgxFileDropEntry,
  FileSystemFileEntry,
  FileSystemDirectoryEntry,
} from 'ngx-file-drop';

@Component({
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.scss'],
})
export class CreateEventComponent implements OnInit {
  event: FormGroup;
  allLocations: Location[];
  errorMessage: string;
  picture: FormGroup;
  url: string;

  //search location
  src: string = '';

  public files: NgxFileDropEntry[] = [];

  constructor(
    private transferService: TransferService,
    private locationService: LocationService,
    private formBuilder: FormBuilder,
    private fileService: FileService,
    private eventService: EventService
  ) {
    this.getLocations();
  }

  ngOnInit(): void {
    //creation form for event
    this.event = new FormGroup({
      title: new FormControl('', [
        Validators.required,
        Validators.minLength(10),
        Validators.maxLength(200),
      ]),
      event_type: new FormControl('news', [Validators.required]),
      location: new FormControl([], [Validators.required]),
      short_description: new FormControl(''),
      description: new FormControl(''),
      active: new FormControl(true),
      image_file_name: new FormControl(null),
    });

    //form for picture
    this.picture = this.formBuilder.group({
      avatar: [],
    });
  }

  onFileChange(picture) {
    if (this.event.get('image_file_name').value) {
      //if user wants to change picture, but one was picked, delete it from server
      this.fileService
        .deleteFile(this.event.get('image_file_name').value)
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
        this.event.get('image_file_name').setValue(res.filename);
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

  createEvent() {
    let formInfo = this.event.value;
    let newEvent: Event = {
      short_description: formInfo.short_description,
      location_id: formInfo.location.id,
      description: formInfo.description,
      event_type: formInfo.event_type,
      title: formInfo.title,
      active: formInfo.active,
    };
    if (formInfo.image_file_name) {
      newEvent.image_file_name = formInfo.image_file_name;
    }

    this.eventService.createEvent(newEvent).subscribe(
      (res) => {
        let event = res;
        this.eventService.getLocationName(event, event.location_id);
        this.transferService.fetchedEvents.push(event);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
    this.event.reset();
    this.picture.get('avatar').setValue(null);
    this.url = '';
    this.src = '';
    this.getLocations();
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }

  getLocations() {
    this.locationService.getLocations().subscribe(
      (res) => {
        this.allLocations = res;
        //set parentName
        this.allLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l);
          }
        });
        this.transferService.setLocations(this.allLocations);
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }
}
