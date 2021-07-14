import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { Auth0Service } from './auth.service';

describe('AuthService', () => {
  let service: Auth0Service;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
    ]
    });
    service = TestBed.inject(Auth0Service);
  });

 /* it('should be created', () => {
    expect(service).toBeTruthy();
  });*/
});
