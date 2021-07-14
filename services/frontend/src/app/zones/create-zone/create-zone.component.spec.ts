import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateZoneComponent } from './create-zone.component';

describe('CreateZoneComponent', () => {
  let component: CreateZoneComponent;
  let fixture: ComponentFixture<CreateZoneComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateZoneComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateZoneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
