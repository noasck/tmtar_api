import { Component, OnInit } from '@angular/core';
import { Auth0Service } from '../shared/services/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  location = localStorage.getItem('user_location_id')
  userInfoFromAuth = JSON.parse(localStorage.getItem('userInfoFromAuth'))
  userName: string
  pictureLink: string

  constructor(private auth: Auth0Service) {
  }

  ngOnInit(): void {
    this.userName = this.userInfoFromAuth.name
    this.pictureLink = this.userInfoFromAuth.picture

    
  }

  logout() {
    this.auth.logout()
  }
}
