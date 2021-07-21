import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpInterceptor,
  HttpHandler,
  HttpRequest,
  HttpErrorResponse,
} from '@angular/common/http';
import { Auth0Service } from '../auth.service';
import { RouterModule } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth: Auth0Service, private route: RouterModule) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    if (this.auth.isAuthenticated()) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${this.auth.getToken()}`,
        },
      });
    }
    return next.handle(request).pipe(
      tap(() => {
        //console.log("intercept")
      }),
      catchError((error: HttpErrorResponse) => {
        console.log('error', error);
        if (error.status === 401) {
          this.auth.refreshToken();
        }
        return throwError(error);
      })
    );
  }
}
