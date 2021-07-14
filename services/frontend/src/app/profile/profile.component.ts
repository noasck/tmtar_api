import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { Location, LocationService } from '../locations/location.service';
import { CurrentUser, UserService } from '../users/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  userInfo: CurrentUser;
  location: Location;
  userInfoFromAuth;
  profile: FormGroup;

  datemask = [/\d/, /\d/, /\d/, /\d/, '-', /\d/, /\d/, '-', /\d/, /\d/];

  filteredLocations: Observable<Location[]>; // for autocomplete
  allLocations: Location[];
  errorMessage: string;

  constructor(
    private locationService: LocationService,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.getLocations();
    this.getFromLocalStorage();
    this.profile = new FormGroup({
      bdate: new FormControl(this.userInfo.bdate),
      sex: new FormControl(this.userInfo.sex),
      place: new FormControl(),
    });
  }

  getFromLocalStorage() {
    this.userInfo = JSON.parse(localStorage.getItem('user_profile'));
    this.userInfoFromAuth = JSON.parse(
      localStorage.getItem('userInfoFromAuth')
    );
  }

  updateProfile() {
    let updateProfile = new Promise((res) => {
      this._updateProfile();
      res(1);
    }).then(() => {
      this.getFromLocalStorage();
      this.getLocations();
    });
  }

  getLocations() {
    this.locationService.getLocations().subscribe(
      (res) => {
        //get user location id
        let userLocationId = +localStorage.getItem('user_location_id');

        this.allLocations = res;

        //set parent name for all location
        this.allLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.setParent(l);
          }
        });

        this.location = this.allLocations.filter(
          (l) => l.id == userLocationId
        )[0];

        this.allLocations = this.allLocations.filter((loc) => loc.id != 1);

        //autocomplete
        this.filteredLocations = this.profile.get('place').valueChanges.pipe(
          startWith(''),
          map((value) => (typeof value === 'string' ? value : value.name)),
          map((name) => (name ? this._filter(name) : this.allLocations.slice()))
        );
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

  _filter(name: string): Location[] {
    const filterValue = name.toLowerCase();

    return this.allLocations.filter(
      (location) => location.name.toLowerCase().indexOf(filterValue) === 0
    );
  }

  _updateProfile() {
    let formInfo = this.profile.value;
    let currentUser: CurrentUser = {};

    if (formInfo.place) {
      currentUser.location_id = formInfo.place.id;
    }
    if (formInfo.bdate) {
      currentUser.bdate = formInfo.bdate;
    }
    if (formInfo.sex) {
      currentUser.sex = formInfo.sex;
    }

    this.userService.updateCurrentUser(currentUser).subscribe(
      (res) => {
        this.userInfo = res;
        localStorage.setItem('user_profile', JSON.stringify(res));
        localStorage.setItem(
          'user_location_id',
          JSON.stringify(res.location_id)
        );
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }
}
