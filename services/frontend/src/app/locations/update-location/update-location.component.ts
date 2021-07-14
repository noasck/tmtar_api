import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from '../location.service';
import { TransferService } from '../../transfer.service';

@Component({
  selector: 'app-update-location',
  templateUrl: './update-location.component.html',
  styleUrls: ['./update-location.component.scss']
})
export class UpdateLocationComponent implements OnInit {
  public location: FormGroup
  errorMsg: string
  allLocations: Location[]
  parent: Location

  @Output() close = new EventEmitter<void>()
  @Input() fetchedLocation: Location

  constructor(private locationService: LocationService, private transferService: TransferService) {
    this.allLocations = this.transferService.locations;
  }



  ngOnInit(): void {

    // get parent of fetchedLocation and create form on component initialization
    this.location = new FormGroup({
      name: new FormControl('', [
        Validators.required
      ])
    })

    this.locationService.getParent(this.fetchedLocation.id).subscribe(
      (res) => {
        this.parent = res;
        console.log(res)
      },
      (error) => {
        this.errorMsg = String(error);
      }, () => {
        this.errorMsg = null;
      }
    )
  }

  editLocation() {
    let data = this.location.value
    const changes = {
      name: data.name
    }

    this.locationService.updateLocation(this.fetchedLocation.id, changes).subscribe(
      (res) => {
        this.allLocations.map((location) => {
          if (location.id == this.fetchedLocation.id) {
            location.name = res.name
          }
        })
        this.transferService.setLocations(this.allLocations)
      },
      (error) => {
        this.errorMsg = String(error);
      }, () => {
        this.errorMsg = null;
      }
    );
  }
}
