import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Params } from '@angular/router';
import { FileSystemDirectoryEntry, FileSystemFileEntry, NgxFileDropEntry } from 'ngx-file-drop';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { FileService } from 'src/app/files/file.service';
import { Location, LocationService } from 'src/app/locations/location.service';
import { TransferService } from 'src/app/transfer.service';
import { Event, EventService } from '../events.service';

@Component({
  selector: 'app-read-event',
  templateUrl: './read-event.component.html',
  styleUrls: ['./read-event.component.scss']
})
export class ReadEventComponent implements OnInit {
  fetchedEvent: Event;
  event: FormGroup
  filteredLocations: Observable<Location[]>;
  allLocations: Location[]
  errorMessage: string
  picture: FormGroup;
  url: string
  oldFileName: string = ""

  eventLocation: Location;
  update: boolean = false
  updatedEvent: boolean = false // for message about update

  public files: NgxFileDropEntry[] = [];

  constructor(private route: ActivatedRoute, private eventService: EventService, private fileService: FileService, private transferService: TransferService, private locationService: LocationService, private formBuilder: FormBuilder) {

  }

  ngOnInit(): void {
    /*this.route.params.subscribe((params: Params)=>{
      this.fetchedEvent = this.transferService.getEventById(params.id)[0]
      console.log(this.event)
    })*/
    //get events for searching 1

    this.route.params.subscribe((params: Params) => {
      this.eventService.getEvents(1).subscribe(
        (res) => {
          this.fetchedEvent = (res.filter((event) => event.id == params.id))[0]
          this.url = this.fetchedEvent.image_file_name ? this.fileService.getFileByName(this.fetchedEvent.image_file_name) : ""

          // get location for autocomplete
          this.locationService.getLocations().subscribe(
            (res) => {
              this.allLocations = res;
              //set parentName
              this.allLocations.map((l) => {
                if (l.id != 1) { this.locationService.getParentName(l) }
              })
              this.eventLocation = res.filter((location) => location.id == this.fetchedEvent.location_id)[0]
              this.transferService.setLocations(this.allLocations);
            },
            (error) => {
              this.errorMessage = error;
            },
            () => {
            }
          );

          this.setEventForm();

        },
        (error) => {
          this.errorMessage = error
        }
      )
    })
    //get locations
  }

  setEventForm() {
    this.event = new FormGroup({
      title: new FormControl(this.fetchedEvent.title, [
        Validators.required
      ]),
      event_type: new FormControl(this.fetchedEvent.event_type, [
        Validators.required
      ]),
      location: new FormControl(this.eventLocation),
      short_description: new FormControl(this.fetchedEvent.short_description, [
        Validators.required
      ]),
      description: new FormControl(this.fetchedEvent.description, [
        Validators.required
      ]),
      active: new FormControl(this.fetchedEvent.active, [
        Validators.required
      ]),
      image_file_name: new FormControl(this.fetchedEvent.image_file_name)
    })

    this.picture = this.formBuilder.group({
      avatar: []
    });

    this.filteredLocations = this.event.get('location').valueChanges
      .pipe(
        startWith(''),
        map(value => typeof value === 'string' ? value : value.name),
        map(name => name ? this._filter(name) : this.allLocations.slice())
      );

  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }
  private _filter(name: string): Location[] {
    const filterValue = name.toLowerCase();

    return this.allLocations.filter(location => location.name.toLowerCase().indexOf(filterValue) === 0);
  }


  onFileChange(picture) {
    if (this.event.get('image_file_name').value) {
      this.oldFileName = this.event.get('image_file_name').value;
      console.log("old", this.oldFileName)
    }

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

  updateEvent() {
    let formInfo = this.event.value

    let newEvent: Event = {
      short_description: formInfo.short_description,
      location_id: formInfo.location ? formInfo.location.id : this.eventLocation.id,
      description: formInfo.description,
      event_type: formInfo.event_type,
      title: formInfo.title,
      active: formInfo.active
    }
    if (formInfo.image_file_name) {
      newEvent.image_file_name = formInfo.image_file_name
    }
    this.eventService.updateEvent(this.fetchedEvent.id, newEvent).subscribe(
      (res) => {
        console.log(res)
        this.fetchedEvent = newEvent;
        this.updatedEvent = true
        this.deleteOldPhoto()
      },
      (error) => {
        this.errorMessage = error;
      }
    )
  }

  deleteOldPhoto() {
    if (this.oldFileName) {
      this.fileService.deleteFile(this.oldFileName).subscribe(
        () => { },
        (error) => {
          this.errorMessage = error;
        }
      );
    }
  }


  public droppedPicture(files: NgxFileDropEntry[]) {
    this.files = files;
    for (const droppedFile of files) {
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          console.log("pic", file)
          this.onFileChange(file)
        });
      } else {
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }
}
