import { Component, OnInit } from '@angular/core';
import { Auth0Service } from '../shared/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private auth: Auth0Service) { 
    auth.handleAuthentication()
    console.log("au", this.auth.isAuthenticated())
  }
  ngOnInit(): void {

  }

  clickLogin(): void {
    this.auth.login()
    /* this.auth.login(this.email).subscribe(
       (token) => {
         console.log('Token Request...');
       },
       (err) => {},
       () => { this.router.navigate(['/'])}
     );*/
  }
}
