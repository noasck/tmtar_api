import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from '../location.service';
import { TransferService } from '../../transfer.service';
import { Observable } from 'rxjs';
export interface User {
  name: string;
}
@Component({
  selector: 'app-create-location',
  templateUrl: './create-location.component.html',
  styleUrls: ['./create-location.component.scss'],
})
export class CreateLocationComponent implements OnInit {
  location: FormGroup;
  errorMessage: string;
  allLocations: Location[];
  parent: Location;
  @Output() close = new EventEmitter<void>();

  src: string = '';

  constructor(
    private locationService: LocationService,
    private transferService: TransferService
  ) {
    this.allLocations = this.transferService.locations;
  }

  ngOnInit(): void {
    this.location = new FormGroup({
      root: new FormControl([], [Validators.required]),
      name: new FormControl('', [Validators.required]),
    });
  }

  createLocation() {
    const index = this.allLocations.reduce(function (prev, current) {
      return prev.id > current.id ? prev : current;
    });

    let data = this.location.value;
    let newLocation = {
      id: index.id + 1,
      name: data.name,
      root: data.root.id,
    };

    this.locationService.createLocation(newLocation).subscribe(
      (response) => {
        response.parentName = data.root.name;
        this.allLocations.push(response);
        this.transferService.setLocations(this.allLocations);

        this.allLocations = this.transferService.locations;
      },

      (error) => {
        this.errorMessage = error;
      },
      () => {
        this.errorMessage = null;
      }
    );
    this.location.reset();
    this.src = '';
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }
}
