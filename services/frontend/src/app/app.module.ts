import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { AuthHttpInterceptor, AuthModule } from '@auth0/auth0-angular';

import { environment as env } from "../environments/environment"

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserComponent } from './users/user/user.component';
import { LocationComponent } from './locations/location/location.component';
import { FileComponent } from './files/file/file.component';
import { UpdateUserComponent } from './users/update-user/update-user.component';
import { CommonModule } from '@angular/common';

//import {httpInterceptorProviders} from './shared/services/http-interceptors';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { UploadFileComponent } from './files/upload-file/upload-file.component';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ReadLocationComponent } from './locations/read-location/read-location.component';
import { UpdateLocationComponent } from './locations/update-location/update-location.component';
import { DeleteLocationComponent } from './locations/delete-location/delete-location.component';
import { SearchPipe } from './shared/search.pipe';
import { LocBoxComponent } from './locations/read-location/loc-box/loc-box.component';
import { CreateLocationComponent } from './locations/create-location/create-location.component';
import { ErrorsComponent } from './errors/errors.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DeleteUserComponent } from './users/delete-user/delete-user.component';
import { AuthGuardService } from './shared/services/auth.guard';
import { Auth0Service } from './shared/services/auth.service';
import { EventsComponent } from './events/events.component';
import { CreateEventComponent } from './events/create-event/create-event.component';
import { ReadEventComponent } from './events/read-event/read-event.component';
import { AuthInterceptor } from './shared/services/http-interceptors/auth.interceptor';
import { NgxFileDropModule } from 'ngx-file-drop';
import { ZonesComponent } from './zones/zones.component';
import { AgmCoreModule } from '@agm/core';
import { AgmJsMarkerClustererModule } from '@agm/js-marker-clusterer';
import { CreateZoneComponent } from './zones/create-zone/create-zone.component';
import { UpdateZoneComponent } from './zones/update-zone/update-zone.component';
import { ProfileComponent } from './profile/profile.component';
import { TextMaskModule } from 'angular2-text-mask';
import { AutocompletePipe } from './shared/autocomplete.pipe';
import { MatNativeDateModule } from '@angular/material/core';
import { MatFormFieldControl } from '@angular/material/form-field';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    //
    UserComponent,
    UpdateUserComponent,
    //
    LocationComponent,
    ReadLocationComponent,
    UpdateLocationComponent,
    DeleteLocationComponent,
    //
    FileComponent,
    HomeComponent,
    UploadFileComponent,
    SearchPipe,
    AutocompletePipe,
    LocBoxComponent,
    CreateLocationComponent,
    ErrorsComponent,
    DeleteUserComponent,
    EventsComponent,
    CreateEventComponent,
    ReadEventComponent,
    ZonesComponent,
    CreateZoneComponent,
    UpdateZoneComponent,
    ProfileComponent
    //
  ],
  imports: [
    CommonModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatAutocompleteModule,
    MatSelectModule,
    MatNativeDateModule,
    TextMaskModule,
    NgxFileDropModule,
    AuthModule.forRoot({
      ...env.auth,
      httpInterceptor: {
        allowedList: [`${env.apiUrl}/`]
      }
    }),
    AgmCoreModule.forRoot({

      apiKey: 'AIzaSyCCBPw6EB0FSx4MkvFMgJ5ZHjKb6iF7ApY',
      libraries: ['places','geometry']

    }),
    AgmJsMarkerClustererModule,
    ReactiveFormsModule.withConfig({warnOnNgModelWithFormControl: 'never'})
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthHttpInterceptor,
    multi: true
  },
  {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true
  }
    , AuthGuardService, Auth0Service],
  bootstrap: [AppComponent]
})
export class AppModule { }
