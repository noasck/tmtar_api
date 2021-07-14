import { Location, LocationService} from './locations/location.service';
import { Injectable } from '@angular/core';
import { User } from './users/user.service';
import { Event } from './events/events.service';

@Injectable({
  providedIn: 'root'
})

export class TransferService {
  locations: Location[]
  users: User[]
  fetchedLocations: Location[];
  errorMessage: string;
  public fetchedEvents: Event[];

  constructor(private locationService: LocationService) { }

  getEvents(){
    return this.fetchedEvents
  }

  getEventById(index): Event[]{
    return this.fetchedEvents.filter((el) => el.id == index)
  }

  setEvents(events: Event[]){
    this.fetchedEvents = events
  }

  setLocations(locs: Location[]){
    this.locations = locs
  }
  
  getLocations(){
    return this.locations
  }

  setUsers(u: User[]){
    this.users = u
  }
  
  getUsers(){
    return this.users
  }

  getLocationFromServer(){
    this.locationService.getLocations().subscribe(
      (res) => {
        this.locations = res;
        //set parentName
        this.locations.map((l) => {
          if(l.id != 1){
            this.setParent(l)
          }
        })
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );

  }

  setParent(location){
    let parent: Location
    this.locationService.getParent(location.id).subscribe(
      (res) => {
        parent = res;
        location.parentName = res.name
      },
      (error) => {
        this.errorMessage = error; 
      }, 
      () => {}
    )
  }

  getParent(id){
    let parent: Location
    this.locationService.getParent(id).subscribe(
      (res) => {
        parent = res;
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    )
    return parent.name
  }

}
