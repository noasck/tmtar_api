import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CreateLocationComponent } from './create-location.component';
import { Location, LocationService } from '../location.service';
import { TransferService } from 'src/app/transfer.service';
import { of } from 'rxjs';

describe('CreateLocationComponent', () => {
  let component: CreateLocationComponent;
  let locationService: LocationService;
  let transferService: TransferService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CreateLocationComponent],
      imports: [
        HttpClientTestingModule
      ]
    })
      .compileComponents();
    locationService = TestBed.inject(LocationService);
    transferService = TestBed.inject(TransferService);
    component = new CreateLocationComponent(locationService, transferService);
  });


  it('should create', () => {
    expect(component).toBeTruthy();
  });


  it('createLocation()', () => {
    let locations: Location[] = [{ id: 1, name: 'root', root: null }, { id: 2, name: 'lviv', root: 1 }, { id: 3, name: 'ukraine', root: 1 }]
    let locationCreated: Location = { id: 4, name: 'dnipro', root: 3 }

    const spy = spyOn(locationService, "createLocation").and.callFake(() => {
      return of(locationCreated)
    })

    component.ngOnInit();
    component.allLocations = locations
    component.location.patchValue({
      root: '3',
      name: 'dnipro'
    });
    component.createLocation()
    expect(spy).toHaveBeenCalled()
  });
});