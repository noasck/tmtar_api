import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpEvent } from '@angular/common/http';
import { EnvironmentUrlService } from './environment-url.service';
import { Observable } from 'rxjs';
import { Auth0Service } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class RepositoryService {
  public accessToken: string;

  constructor(
    private http: HttpClient,
    private envUrl: EnvironmentUrlService,
    private auth: Auth0Service
  ) {}

  public getData<T>(route: string): Observable<T> {
    return this.http.get<T>(
      this.createCompleteRoute(route, this.envUrl.apiUrl),
      { headers: this.generateHeaders() }
    );
  }

  public create<T>(route: string, body): Observable<T> {
    return this.http.post<T>(
      this.createCompleteRoute(route, this.envUrl.apiUrl),
      body,
      { headers: this.generateHeaders() }
    );
  }

  public update<T>(route: string, body): Observable<T> {
    return this.http.put<T>(
      this.createCompleteRoute(route, this.envUrl.apiUrl),
      body,
      { headers: this.generateHeaders() }
    );
  }

  public delete<T>(route: string): Observable<T> {
    return this.http.delete<T>(
      this.createCompleteRoute(route, this.envUrl.apiUrl),
      { headers: this.generateHeaders() }
    );
  }

  private createCompleteRoute = (route: string, envAddress: string) => {
    return `${envAddress}/${route}`;
  };

  private generateHeaders(): HttpHeaders {
    return new HttpHeaders({});
    //no auth header, bc in interceptor
  }
}
