import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { UserService } from '../user.service';
import { Auth0Service } from 'src/app/shared/services/auth.service';
import { RouterModule } from '@angular/router';
import { AuthModule } from '@auth0/auth0-angular';
import { environment as env } from 'src/environments/environment';
import users from '../../shared/mockDB/users.js';

import locations from '../../shared/mockDB/locations';
import { EMPTY, of, throwError } from 'rxjs';
import { UpdateUserComponent } from './update-user.component';
import { LocationService } from 'src/app/locations/location.service';

describe('UserComponent', () => {
  let userService: UserService;
  let locationService: LocationService;
  let component: UpdateUserComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterModule.forRoot([
          { path: 'users', component: UpdateUserComponent },
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

    locationService = TestBed.inject(LocationService);
    userService = TestBed.inject(UserService);
    component = new UpdateUserComponent(userService, locationService);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should create form with one control', () => {
    component.ngOnInit();
    expect(component.user.contains('admin_location')).toBe(true);

  });

  it('should upload available locations for user', () => {
    const spy = spyOn(locationService, 'getLocations').and.returnValue(of(locations));

    component.ngOnInit();
    
    expect(spy).toHaveBeenCalled();
  });

  it('should update user admin location', () => {
    let updatedUser = {
      admin_location_id: 2,
      sex: null,
      identity: 'auth0|609fd1ff3872bb0068e63812',
      id: 5,
      bdate: null,
      location_id: 5,
    };

    spyOn(userService, 'updateUser').and.callFake(() => {
      return of(updatedUser);
    });

    component.ngOnInit();
    component.fetchedUser = users[1];

    component.user.patchValue({
      admin_location: locations[0],
    });

    component.updateUser();

    expect(component.fetchedUser.admin_location_id).toEqual(
      updatedUser.admin_location_id
    );
  });

  it('should set errorMessage if was error when updating user', () => {
    let error = 'Error Message';
    spyOn(userService, 'updateUser').and.returnValue(throwError(error));

    component.ngOnInit();
    component.fetchedUser = users[1];

    component.user.patchValue({
      admin_location: locations[0],
    });

    component.updateUser();

    expect(component.errorMessage).toBe(error);
  });

  /*
  it('get all users', () => {
    spyOn(service, 'getUsers').and.callFake(() => {
      return of(users);
    });

    component.ngOnInit();
    let fetchedUsers = component.fetchedUsers;
    expect(fetchedUsers).toBe(users);
  });

  it('should set errorMessage id error when getting users', () => {
    let error = 'Error message';
    spyOn(service, 'getUsers').and.returnValue(throwError(error));

    component.ngOnInit();
    expect(component.errorMessage).toBe(error);
  });

  it('delete user', () => {
    let spy = spyOn(service, 'deleteUserByID').and.returnValue(EMPTY);

    component.ngOnInit();
    component.deleteUser(true, 5);

    expect(spy).toHaveBeenCalledWith(5);
  });*/
});
