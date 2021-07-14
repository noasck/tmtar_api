import { HttpClientTestingModule } from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";
import { EMPTY, of } from "rxjs";
import { LocationService } from "src/app/locations/location.service";
import { TransferService } from "src/app/transfer.service";
import { User, UserService } from "../user.service";
import { UpdateUserComponent } from "./update-user.component";

describe('UpdateUserComponent', () => {
  let service: UserService;
  let locationService: LocationService;
  let transferService: TransferService;
  let component: UpdateUserComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ]
    });

    service = TestBed.inject(UserService);
    locationService = TestBed.inject(LocationService);
    transferService = TestBed.inject(TransferService);
    component = new UpdateUserComponent(service, transferService);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should create form control admin_location', () => {
    component.ngOnInit();
    expect(component.user.contains('admin_location')).toBeTruthy();
  });

  it('update()', () => {
    let userUpdated: User = { "bdate": null, "id": 228, "admin_location_id": 3, "location_id": 1, "sex": null }
    let data: User = { "bdate": null, "id": 228, "admin_location_id": 1, "location_id": 1, "sex": null }

    const spy = spyOn(service, "updateUser").and.callFake(() => {
      return of(userUpdated)
    })
    component.fetchedUser = data
    component.ngOnInit();
    component.user.patchValue({
      admin_location: 3
    });
    component.update()
    expect(spy).toHaveBeenCalled()
  });

});
