import { Component, OnInit } from '@angular/core';
import { LocationService } from '../locations/location.service';
import { Auth0Service } from '../shared/services/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  location = +localStorage.getItem('user_location_id');
  userInfoFromAuth = JSON.parse(localStorage.getItem('userInfoFromAuth'));
  userName: string;
  pictureLink: string;
  locationName: string;

  errorMessage: string;

  constructor(
    private auth: Auth0Service,
    private locationService: LocationService
  ) {}

  ngOnInit(): void {
    this.userName = this.userInfoFromAuth.name;
    this.pictureLink = this.userInfoFromAuth.picture;

    this.getAdminLocation();
  }

  logout() {
    this.auth.logout();
  }

  getAdminLocation() {
    this.locationService.getLocationsByID(this.location).subscribe(
      (res) => {
        this.locationName = res.name;
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }
}
