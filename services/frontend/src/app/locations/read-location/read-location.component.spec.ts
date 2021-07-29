import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Auth0Service } from 'src/app/shared/services/auth.service';
import { RouterModule } from '@angular/router';
import { AuthModule } from '@auth0/auth0-angular';
import { environment as env } from 'src/environments/environment';
import { LocationService } from '../location.service.js';
import { ReadLocationComponent } from './read-location.component.js';
import locations from '../../shared/mockDB/locations.js';
import { of } from 'rxjs';

describe('LocationComponent', () => {
  let service: LocationService;
  let component: ReadLocationComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterModule.forRoot([
          { path: 'locations/read', component: ReadLocationComponent },
        ]),
        AuthModule.forRoot({
          ...env.auth,
          httpInterceptor: {
            allowedList: [`${env.apiUrl}/`],
          },
        }),
      ],
      providers: [Auth0Service],
    });

    service = TestBed.inject(LocationService);
    component = new ReadLocationComponent(service);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('get all locations', () => {
    spyOn(service, 'getLocations').and.callFake(() => {
      return of(locations);
    });

    component.ngOnInit();
    let fetchedLocations = component.fetchedLocations;
    expect(fetchedLocations.length).toBe(locations.length);
  });
});
