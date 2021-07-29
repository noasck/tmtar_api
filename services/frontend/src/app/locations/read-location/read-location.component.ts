import { Component, OnInit } from '@angular/core';
import { Location, LocationService } from '../location.service';

@Component({
  selector: 'app-read-location',
  templateUrl: './read-location.component.html',
  styleUrls: ['./read-location.component.scss'],
})
export class ReadLocationComponent implements OnInit {
  parent: Location;
  fetchedLocations: Location[];
  fetched: boolean;
  locShown: boolean;
  errorMessage: string;
  pay: boolean = false;

  create: boolean = false;

  constructor(private locationService: LocationService) {}

  public ngOnInit(): void {
    // get all locations on component initialization
    this.fetched = false;
    this.getLocations();
  }

  getLocations() {
    this.locationService.getLocations().subscribe(
      (res) => {
        this.fetchedLocations = res;
        //set parentName
        this.fetchedLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l);
          }
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {
        this.fetched = true;
      }
    );
  }
}
