import { Injectable, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { RepositoryService } from 'src/app/shared/services/repository.service';
import { LocationService } from '../locations/location.service';
export interface Event {
  update_date?: number,
  short_description: string,
  location_id?: number,
  description?: string,
  event_type?: string,
  image_file_name?: string,
  id?: number,
  title: string,
  active?: boolean,

  locationName?: string, //
  parentLocationName?: string //
}

export interface Count {
  count: number
}

export interface SearchEvents {
  events: Event[],
  status: string
}

@Injectable({
  providedIn: 'root',
})
export class EventService {
  route = 'events/';
  constructor(public repository: RepositoryService, private locationService: LocationService) { }

  getEvents(page): Observable<Event[]> {
    return this.repository.getData<Event[]>(this.route + `all/${page}`);
  }

  countEvents(): Observable<Count> {
    return this.repository.getData<Count>(this.route + `all/count`);
  }

  updateEvent(id: number, Event: Event): Observable<Event> {
    return this.repository.update<Event>(this.route + String(id), Event);
  }

  search(str: string) {
    return this.repository.getData<SearchEvents>(this.route + "all/search/" + str);
  }

  deleteEventById(id: number): Observable<null> {
    return this.repository.delete<null>(this.route + String(id));
  }

  createEvent(Event: Event): Observable<Event> {
    return this.repository.create<Event>(this.route, Event);
  }

  getLocationName(event, id): void {
    this.locationService.getLocationsByID(id).subscribe(
      (res) => {
        event.locationName = res.name
      },
      (error) => {
        //this.errorMessage = String(error);
      }, () => {
        //this.errorMessage = null;
      }
    )

    this.locationService.getParent(id).subscribe(
      (res) => {
        event.parentLocationName = res.name
      },
      (error) => {
        // this.errorMessage = String(error);
      }, () => {
        //this.errorMessage = null;
      }
    )
  }
}
