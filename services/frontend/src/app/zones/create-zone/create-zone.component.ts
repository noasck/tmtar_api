import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { Location, LocationService } from 'src/app/locations/location.service';
import { Zone, ZonesService } from '../zones.service';

@Component({
  selector: 'app-create-zone',
  templateUrl: './create-zone.component.html',
  styleUrls: ['./create-zone.component.scss'],
})
export class CreateZoneComponent implements OnInit {
  zone: FormGroup;

  allLocations: Location[];
  errorMessage: string;

  //search location
  src: string = '';

  @Input() fetchedCoordinates: any; // object {lat:  number, lng: number}
  @Output() close = new EventEmitter<void>();
  @Output() create = new EventEmitter<Zone>();

  constructor(
    private zoneService: ZonesService,
    private locationService: LocationService
  ) {
    this.getLocations();
  }

  ngOnInit(): void {
    this.setZoneForm();
  }

  setZoneForm() {
    this.zone = new FormGroup({
      longitude: new FormControl(this.fetchedCoordinates.lng, [
        Validators.required,
        Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/),
      ]),
      latitude: new FormControl(this.fetchedCoordinates.lat, [
        Validators.required,
        Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/),
      ]),
      radius: new FormControl(null, [Validators.required]),
      title: new FormControl('', [
        Validators.required,
        Validators.minLength(6),
        Validators.maxLength(100),
      ]),
      active: new FormControl(true, [Validators.required]),
      secret: new FormControl(false, [Validators.required]),
      location: new FormControl({}, [Validators.required]),
    });
  }

  createZone() {
    let z = this.zone.value;
    let newZone = {
      title: z.title,
      latitude: z.latitude,
      longitude: z.longitude,
      radius: z.radius,
      location_id: z.location.id,
      active: z.active,
      secret: z.secret,
    };
    this.zoneService.createZone(newZone).subscribe(
      (res) => {
        this.create.emit(res);
        this.close.emit();
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );

    this.zone.reset();
    this.src = ''
  }

  getLocations() {
    this.locationService.getLocations().subscribe(
      (res) => {
        //get user location id
        let userLocationId = +localStorage.getItem('user_location_id');

        //get all children locations for user location
        this.allLocations = this.locationService.getLocationChildren(
          res,
          userLocationId
        );

        //set parent name for all location
        this.allLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l);
          }
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }
}
