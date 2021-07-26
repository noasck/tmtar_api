import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from 'src/app/locations/location.service';
import { Zone, ZonesService } from '../zones.service';

@Component({
  selector: 'app-update-zone',
  templateUrl: './update-zone.component.html',
  styleUrls: ['./update-zone.component.scss'],
})
export class UpdateZoneComponent implements OnInit {
  zone: FormGroup;

  allLocations: Location[];
  errorMessage: string;

  zoneLocation: Location;

  //search location
  src: string = '';

  @Input() fetchedZone: Zone; //zone for update
  @Input() coordinates?: any; // object {lat:  number, lng: number}
  @Output() close = new EventEmitter<void>();
  @Output() update: EventEmitter<any> = new EventEmitter<void>();

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
      longitude: new FormControl(
        this.coordinates ? this.coordinates.lng : this.fetchedZone.longitude,
        [Validators.required, Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/)]
      ),
      latitude: new FormControl(
        this.coordinates ? this.coordinates.lat : this.fetchedZone.latitude,
        [Validators.required, Validators.pattern(/^\-?\d+((\.|\,)\d+)?$/)]
      ),
      radius: new FormControl(this.fetchedZone.radius, [Validators.required]),
      title: new FormControl(this.fetchedZone.title, [
        Validators.required,
        Validators.minLength(6),
        Validators.maxLength(100),
      ]),
      active: new FormControl(this.fetchedZone.active, [Validators.required]),
      secret: new FormControl(this.fetchedZone.secret, [Validators.required]),
      location: new FormControl(this.zoneLocation),
    });
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

        this.setZoneLocation(this.fetchedZone.location_id)
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  updateZone() {
    let formData = this.zone.value;
    let update = {
      title: formData.title,
      latitude: formData.latitude,
      longitude: formData.longitude,
      radius: formData.radius,
      location_id: formData.location
        ? formData.location.id
        : this.fetchedZone.location_id,
      active: formData.active,
      secret: formData.secret,
    };
    this.zoneService.updateZone(this.fetchedZone.id, update).subscribe(
      (res) => {
        this.fetchedZone = res;
        this.update.emit(res);
      },
      (error) => {
        this.errorMessage = error;
      }
    );

    this.src = '';
    this.setZoneLocation(this.fetchedZone.location_id)

  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }

  setZoneLocation(id){
    this.zoneLocation = this.allLocations.filter(
      (location) => location.id == this.fetchedZone.location_id
    )[0];
  }
}
