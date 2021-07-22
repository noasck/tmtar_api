/*import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { TransferService } from 'src/app/transfer.service';
import { Location, LocationService } from '../location.service';

import { UpdateLocationComponent } from './update-location.component';

describe('UpdateLocationComponent', () => {
  let component: UpdateLocationComponent;
  let locationService: LocationService;
  let transferService: TransferService;
  let fixture: ComponentFixture<UpdateLocationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UpdateLocationComponent],
      imports: [
        HttpClientTestingModule,
      ]
    })
      .compileComponents();
    locationService = TestBed.inject(LocationService);
    transferService = TestBed.inject(TransferService);
    component = new UpdateLocationComponent(locationService, transferService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('editLocation()', () => {
    let locations: Location[] = [{ id: 1, name: 'root', root: null }, { id: 2, name: 'lviv', root: 1 }, { id: 3, name: 'ukraine', root: 1 }]
    let locationUpdated: Location = { id: 2, name: 'kherson', root: 3 }
    let data: Location = { id: 2, name: 'lviv', root: 1 }

    const spy = spyOn(locationService, "updateLocation").and.callFake(() => {
      return of(locationUpdated)
    })
    component.fetchedLocation = data
    component.ngOnInit();
    component.allLocations = locations
    component.location.patchValue({
      name: 'kherson'
    });
    component.editLocation()
    expect(spy).toHaveBeenCalled()
  });

});*/
