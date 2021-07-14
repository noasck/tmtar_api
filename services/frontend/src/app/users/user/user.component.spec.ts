import { HttpClientTestingModule } from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";
import { EMPTY, of } from "rxjs";
import { LocationService } from "src/app/locations/location.service";
import { TransferService } from "src/app/transfer.service";
import { User } from "src/app/_models/user";
import { UserService } from "../user.service";
import { UserComponent } from "./user.component";

describe('UserComponent', () => {
  let service: UserService;
  let locationService: LocationService;
  let transferService: TransferService;
  let component: UserComponent;
  let users: User[] = [{ "bdate": null, "id": 228, "email": "denter425@gmail.com", "admin_location_id": 0, "location_id": 1, "sex": null }]

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
    expect(component).toBeTruthy();
  });

  it('ngOnInit()', () => {
    const spy = spyOn(service, "getUsers").and.callFake(() => {
      return EMPTY
    })
    component.ngOnInit()
    expect(spy).toHaveBeenCalled()
  });

  it('sould calculate length of Users[] from ngOnInit()', () => {
    spyOn(service, "getUsers").and.callFake(() => {
      return of(users)
    })
    component.ngOnInit()
    let fetchedUsers = component.fetchedUsers
    expect(fetchedUsers.length).toBe(users.length)
  });

  it('deleteUser()', () => {
    const spy = spyOn(service, "deleteUserByID").and.callFake(() => {
      return EMPTY
    })
    component.deleteUser(true, 228)
    expect(spy).toHaveBeenCalled()
  });

});
