import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReadLocationComponent } from './read-location.component';
import { Location, LocationService } from '../location.service';
import { TransferService } from 'src/app/transfer.service';
import { EMPTY, of } from 'rxjs';
import { LocBoxComponent } from './loc-box/loc-box.component';

describe('ReadLocationComponent', () => {
  let component: ReadLocationComponent;
  let locComponent: LocBoxComponent
  let locationService: LocationService;
  let transferService: TransferService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReadLocationComponent],
      imports: [
        HttpClientTestingModule
      ]
    })
      .compileComponents();
    locationService = TestBed.inject(LocationService);
    transferService = TestBed.inject(TransferService);
    component = new ReadLocationComponent(locationService, transferService);
    locComponent = new LocBoxComponent(transferService, locationService)
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit()', () => {
    let locations: Location[] = [{ id: 1, name: 'root', root: null }, { id: 2, name: 'lviv', root: 1 }, { id: 3, name: 'ukraine', root: 1 }]

    const spy = spyOn(locationService, "getLocations").and.callFake(() => {
      return of(locations)
    })
    component.ngOnInit()
    expect(spy).toHaveBeenCalled()
  });

  it('deleteLocation()', () => {
    const spy = spyOn(locationService, "deleteLocationByID").and.callFake(() => {
      return EMPTY
    })
    locComponent.deleteLocation(true, null)
    expect(spy).toHaveBeenCalled()
  });
});