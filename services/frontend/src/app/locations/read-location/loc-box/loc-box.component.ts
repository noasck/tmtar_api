import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import { Location, LocationService } from '../../location.service';
import { TransferService } from '../../../transfer.service';
@Component({
  selector: 'app-loc-box',
  templateUrl: './loc-box.component.html',
  styleUrls: ['./loc-box.component.scss'],
})
export class LocBoxComponent implements OnInit {
  locationChange: Location;
  deleteLoc: Location;
  errorMessage: string;
  places = {};
  showLocs = {};
  children = {};

  @Input() locationRoot: number;
  @Input() show: boolean;
  @Input() allLocations: Location[];

  constructor(
    private transferService: TransferService,
    private locationService: LocationService
  ) {}

  ngOnInit(): void {
    this.allLocations = this.transferService.getLocations();
  }

  showLocation(locationId) {
    //open/close(show) location from root
    this.places[locationId] = locationId;
    this.showLocs[locationId] = !this.showLocs[locationId];
  }

  deleteLocation(delOption, deleteId) {
    if (delOption) {
      this.locationService.deleteLocationByID(deleteId).subscribe(
        () => {
          this.allLocations = this.allLocations.filter(
            (user) => user.id != deleteId
          );
          this.transferService.setLocations(this.allLocations);
        },
        (error) => {
          this.errorMessage = error;
        }
      );
    }
    this.deleteLoc = null;
  }
}
