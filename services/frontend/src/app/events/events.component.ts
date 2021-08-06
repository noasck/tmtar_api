import { Component, OnInit, SimpleChanges } from '@angular/core';
import { FileService } from '../files/file.service';
import { TransferService } from '../transfer.service';
import { Count, Event, EventService } from './events.service';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.scss'],
})
export class EventsComponent implements OnInit {
  fetchedEvents: Event[];
  errorMessage: string;
  deleteEvent: Event;
  eventCounter: number = 1;
  page: number = 1;
  searchEvent: string = '';

  constructor(
    private eventService: EventService,
    private transferService: TransferService,
    private fileService: FileService
  ) {}

  ngOnInit(): void {
    this.countEvents();
    this.getEvents(this.page);
  }

  searchEventByTitle() {
    if (this.searchEvent) {
      setTimeout(() => {
        this.eventService.search(this.searchEvent).subscribe(
          (res) => {
            this.fetchedEvents = res.events;
            this.fetchedEvents.map((event) => {
              this.eventService.getLocationName(event, event.location_id);
            });
            this.transferService.setEvents(this.fetchedEvents);
          },
          (error) => {
            this.errorMessage = error;
          }
        );
      }, 2000);
    } else {
      this.ngOnInit()
    }
  }

  getEvents(p) {
    this.page = p;
    this.eventService.getEvents(p).subscribe(
      (res) => {
        this.fetchedEvents = res;
        this.fetchedEvents.map((event) => {
          this.eventService.getLocationName(event, event.location_id);
        });
        this.fetchedEvents.sort(this.byField('update_date'));
        this.transferService.setEvents(this.fetchedEvents);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }

  countEvents() {
    this.eventService.countEvents().subscribe(
      (res) => {
        this.eventCounter = Math.ceil(res.count / 10);
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  deleteEventById(id: number) {
    this.eventService.deleteEventById(id).subscribe(
      () => {
        this.fetchedEvents = this.fetchedEvents.filter(
          (event) => event.id != id
        );
        this.transferService.setEvents(this.fetchedEvents);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
    this.deleteEvent = null;
  }

  getFileLink(filename: string) {
    return this.fileService.getFileByName(filename);
  }

  byField(field) {
    return (a, b) => (a[field] > b[field] ? 1 : -1);
  }
}
