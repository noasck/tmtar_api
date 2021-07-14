import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UpdateZoneComponent } from './update-zone.component';

describe('ZoneUpdateComponent', () => {
  let component: UpdateZoneComponent;
  let fixture: ComponentFixture<UpdateZoneComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateZoneComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateZoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
