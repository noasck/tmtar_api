import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { User, UserService } from '../user.service';
import { UserComponent } from './user.component';
import { Auth0Service } from 'src/app/shared/services/auth.service';
import { RouterModule } from '@angular/router';
import { AuthModule } from '@auth0/auth0-angular';
import { environment as env } from 'src/environments/environment';
import users from '../../shared/mockDB/users.js';
import { EMPTY, of, throwError } from 'rxjs';

describe('UserComponent', () => {
  let service: UserService;
  let component: UserComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterModule.forRoot([{ path: 'users', component: UserComponent }]),
        AuthModule.forRoot({
          ...env.auth,
          httpInterceptor: {
            allowedList: [`${env.apiUrl}/`],
          },
        }),
      ],
      providers: [Auth0Service],
    });

    service = TestBed.inject(UserService);
    component = new UserComponent(service);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('get all users', () => {
    spyOn(service, 'getUsers').and.callFake(() => {
      return of(users);
    });

    component.ngOnInit();
    let fetchedUsers = component.fetchedUsers;
    expect(fetchedUsers).toBe(users);
  });

  it('should set errorMessage if error when getting users', () => {
    let error = 'Error message';
    spyOn(service, 'getUsers').and.returnValue(throwError(error));

    component.ngOnInit();
    expect(component.errorMessage).toBe(error);
  });

  it('delete user', () => {
    component.fetchedUsers = users;
    let spy = spyOn(service, 'deleteUserByID').and.returnValue(EMPTY);

    component.ngOnInit();
    component.deleteUser(true, 5);

    expect(spy).toHaveBeenCalledWith(5);
  });
});
