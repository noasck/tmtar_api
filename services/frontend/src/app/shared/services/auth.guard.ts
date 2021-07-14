import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot } from '@angular/router';
import { Auth0Service } from './auth.service';

@Injectable()
export class AuthGuardService implements CanActivate {

  constructor(public auth0: Auth0Service, public router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {

    if (!this.auth0.isAuthenticated()) {
      this.router.navigate(['/login']);
      return false;
    }
    return true;
  }

}




/*import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(
        private router: Router,
        private authService: AuthService
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        const currentUser = this.authService.currentUserValue;
        if (currentUser) {
            // logged in so return true
            return true;
        }

        // not logged in so redirect to login page with the return url
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
        return false;
    }
}
*/