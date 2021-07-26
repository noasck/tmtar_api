import { Component, OnInit } from '@angular/core';
import { MouseEvent } from '@agm/core';
import { Zone, ZonesService } from './zones.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from '../locations/location.service';

interface marker {
  latitude: number;
  longitude: number;
  title: string;
}

@Component({
  selector: 'app-zones',
  templateUrl: './zones.component.html',
  styleUrls: ['./zones.component.scss'],
})
export class ZonesComponent implements OnInit {
  fetchedZones: Zone[] = [];
  errorMessage: string;
  zone: FormGroup;

  delZone: marker = null; //open deletion
  zoneForUpdate: Zone = null;
  newCoorditanes: any = null;
  coordinatesForCreation: any = null;

  src = ''; //search zone
  allLocations: Location[];

  //map config
  zoom: number = 6;
  gridSize: number = 100;
  mode: string = 'view';

  // initial center position for the map
  latitude: number = 49;
  longitude: number = 32;

  constructor(
    private zoneService: ZonesService,
    private locationService: LocationService
  ) {}

  ngOnInit() {
    let getLocs = new Promise((resolve) => {
      this.getLocations();
      this.getAllZones();
      resolve(1);
    }).then(() => {
      let numberOfZones = this.fetchedZones.length;
      this.gridSize = Math.round(
        30 * Math.tanh((numberOfZones - 10000) / 20000) + 95
      );
    });
  }

  getAllZones() {
    this.zoneService.getZones().subscribe(
      (res) => {
        this.fetchedZones = res;
        this.fetchedZones.map((zone) => {
          zone.draggable = true;
          zone.location = this.getZoneLocation(zone.location_id);
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  clickedMarker(label: string, index: number) {
    console.log(`clicked the marker: ${label || index}`);
  }

  mapClicked($event: MouseEvent) {
    if (this.mode == 'create') {
      this.coordinatesForCreation = $event.coords;
    }
  }

  addZone(newZone) {
    newZone.location = this.getZoneLocation(newZone.location_id);
    this.fetchedZones.push(newZone);
  }

  markerDragEnd(m: Zone, $event: MouseEvent) {
    this.newCoorditanes = $event.coords;
    this.zoneForUpdate = m;
    //update this Zone
  }

  deleteZone(id) {
    this.zoneService.deleteZoneByID(id).subscribe(
      () => {
        this.fetchedZones = this.fetchedZones.filter((zone) => zone.id != id);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }

  updateZones() {
    this.getAllZones();
  }

  zoomZone(zone) {
    this.latitude = zone.latitude;
    this.longitude = zone.longitude;
    this.zoom = 9;
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

  getZoneLocation(locId) {
    let location = this.allLocations.filter((l) => l.id == locId)[0];
    return location;
  }
}

/* let max_long = 90;
     let min_long = -90;
     let max_lat = 90;
     let min_lat = -90;
     for(let i = 1; i<=25000; i++){
       this.fetchedZones.push(
         {
           lat: Math.random() * (max_long - min_long) + min_long,
           long: Math.random() * (max_lat - min_lat) + min_lat,
           name: `${i}`,
           draggable: true
         }
       )
     }*/
