import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from '../location.service';
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
  parent: Location;

  @Input() allLocations: Location[];
  @Output() close = new EventEmitter<void>();

  src: string = '';

  constructor(private locationService: LocationService) {}

  ngOnInit(): void {
    this.location = new FormGroup({
      root: new FormControl([], [Validators.required]),
      name: new FormControl('', [Validators.required]),
    });
  }

  createLocation() {
    let data = this.location.value;
    let newLocation = {
      name: data.name,
      root: data.root.id,
    };

    this.locationService.createLocation(newLocation).subscribe(
      (response) => {
        response.parentName = data.root.name;
        this.allLocations.push(response);
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
