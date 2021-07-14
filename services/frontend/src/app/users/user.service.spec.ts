import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Location, LocationService } from '../locations/location.service';
import { TransferService } from '../transfer.service';
import { User } from '../_models/user';

import { UserService } from './user.service';
import { UserComponent } from './user/user.component';

describe('UserService', () => {
  let service: UserService;
  let locationService: LocationService;
  let transferService: TransferService;
  let component: UserComponent;
  let users: User[] = [{ "bdate": null, "id": 228, "email": "denter425@gmail.com", "admin_location_id": 0, "location_id": 1, "sex": null }, { "bdate": null, "id": 1337, "email": "jjok730@gmail.com", "admin_location_id": 0, "location_id": 2, "sex": null }]
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ]
    });

    service = TestBed.inject(UserService);
    locationService = TestBed.inject(LocationService);
    transferService = TestBed.inject(TransferService);
    component = new UserComponent(service, locationService, transferService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

});
