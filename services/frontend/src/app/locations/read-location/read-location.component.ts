import { Component, OnInit } from '@angular/core';
import { Location, LocationService } from '../location.service';
import { TransferService } from '../../transfer.service';


@Component({
  selector: 'app-read-location',
  templateUrl: './read-location.component.html',
  styleUrls: ['./read-location.component.scss']
})
export class ReadLocationComponent implements OnInit {
  parent: Location
  fetchedLocations: Location[];
  fetched: boolean;
  locShown: boolean;
  errorMessage: string;
  pay: boolean = false

  create: boolean = false

  constructor(private locationService: LocationService, private transferService: TransferService) {
  }

  public ngOnInit(): void {
    // get all locations on component initialization
    this.fetched = false;
    this.locationService.getLocations().subscribe(
      (res) => {
        this.fetchedLocations = res;
        //set parentName
        this.fetchedLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l)
          }
        })
        this.transferService.setLocations(this.fetchedLocations);
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
