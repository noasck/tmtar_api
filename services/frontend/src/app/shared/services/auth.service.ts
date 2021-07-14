import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import auth0 from 'auth0-js';
import { AuthService } from '@auth0/auth0-angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { User } from 'src/app/users/user.service';

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  status: string;
}

@Injectable()
export class Auth0Service {
  tokenResponse: AuthResponse;
  userProfile: any;
  requestedScopes: string = 'openid';

  auth0 = new auth0.WebAuth({
    domain: 'supruniiuk.us.auth0.com',
    clientID: 'WZOJ7xNMIVcU1uI90oPkY9m8bN8GNIHT',
    audience: 'takemetoarapi',
  });

  constructor(
    public router: Router,
    public auth: AuthService,
    private http: HttpClient
  ) {}

  public login(): void {
    this.auth0.authorize({
      audience: 'takemetoarapi',
      scope: 'openid profile email',
      responseType: 'token id_token',
      redirectUri: 'http://localhost:4200/login',
    });
  }

  public handleAuthentication(): void {
    this.auth0.parseHash((err, authResult) => {
      if (authResult && authResult.accessToken && authResult.idToken) {
        window.location.hash = '';
        this.setSession(authResult);
        this.router.navigate(['']);
      } else if (err) {
        this.router.navigate(['']);
        //console.log(err);
        alert(
          'Error: <%= "${err.error}" %>. Check the console for further details.'
        );
      }
    });
  }

  private setSession(authResult): void {
    const expiresAt = JSON.stringify(
      authResult.expiresIn * 1000 + new Date().getTime()
    );
    const scopes = authResult.scope || this.requestedScopes || '';
    localStorage.setItem("userInfoFromAuth", JSON.stringify(authResult.idTokenPayload))
    localStorage.setItem('access_token', authResult.accessToken);
    localStorage.setItem('id_token', authResult.idToken);
    localStorage.setItem('expires_at', expiresAt);
    localStorage.setItem('scopes', JSON.stringify(scopes));

    //console.table(localStorage)

    if (!environment.production) {
      localStorage.setItem(
        'access_token',
        'google-oauth2|112161506929078504169'
      );
    }

    this.loginApi();
  }

  public logout(): void {
    localStorage.clear();
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  public isAuthenticated(): boolean {
    const expiresAt = JSON.parse(localStorage.getItem('expires_at'));
    return new Date().getTime() < expiresAt;
  }

  public userHasScopes(scopes: Array<string>): boolean {
    const grantedScopes = JSON.parse(localStorage.getItem('scopes')).split(' ');
    return scopes.every((scope) => grantedScopes.includes(scope));
  }

  public getToken() {
    return localStorage.getItem('access_token');
  }

  public loginApi() {
    let token = this.getToken();
    this.http
      .get<any>(`${environment.apiUrl}` + `/users/login`, {
        headers: this.generateHeaders(token),
      })
      .subscribe(
        (res) => {
          this.tokenResponse = res;
          localStorage.setItem('access_token', res.access_token);
          localStorage.setItem('refresh_token', res.refresh_token);

          this.getUserProfile()
        },
        (error) => {
          console.log('error', error);
        }
      );
  }

  getUserProfile(){
    let token = this.getToken();
    this.http.get<User>(`${environment.apiUrl}` + `/users/profile`, {
        headers: this.generateHeaders(token),
      })
      .subscribe(
          (res) => {
              localStorage.setItem('user_profile', JSON.stringify(res))
              localStorage.setItem('user_location_id', JSON.stringify(res.location_id))
              console.log(JSON.parse(localStorage.getItem('user_location_id')))
          },
          (error) => {
            console.log('error', error);
          }
      )
  }

  public refreshToken() {
    let newToken = localStorage.getItem('refresh_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.setItem('access_token', newToken);
    this.loginApi();
  }

  private generateHeaders(token): HttpHeaders {
    return new HttpHeaders({
      authorization: `Bearer ${token}`,
    });
  }
}
