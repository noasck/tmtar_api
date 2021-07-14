import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LocationComponent } from './locations/location/location.component';
import { UserComponent } from './users/user/user.component';
import { FileComponent } from './files/file/file.component';
import { AuthGuardService } from './shared/services/auth.guard';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { UploadFileComponent } from './files/upload-file/upload-file.component';
import { ReadLocationComponent } from './locations/read-location/read-location.component';
import { UpdateLocationComponent } from './locations/update-location/update-location.component';
import { DeleteLocationComponent } from './locations/delete-location/delete-location.component';
import { UpdateUserComponent } from './users/update-user/update-user.component';
import { CreateLocationComponent } from './locations/create-location/create-location.component';
import { EventsComponent } from './events/events.component';
import { ReadEventComponent } from './events/read-event/read-event.component';
import { CreateEventComponent } from './events/create-event/create-event.component';
import { ZonesComponent } from './zones/zones.component';
import { ProfileComponent } from './profile/profile.component';

const routes: Routes = [
  {
    path: '', component: HomeComponent, canActivate: [AuthGuardService], children: [
      {
        path: 'profile', component: ProfileComponent 
      },
      {
        path: 'users', component: UserComponent, children: [{
          path: 'update', component: UpdateUserComponent
        }
        ]
      },
      {
        path: 'files', component: FileComponent, children: [
          {
            path: 'create', component: UploadFileComponent
          }
        ]
      },
      {
        path: 'locations', component: LocationComponent, children: [{
          path: 'read', component: ReadLocationComponent
        },
        {
          path: 'update', component: UpdateLocationComponent
        },
        {
          path: 'delete', component: DeleteLocationComponent
        },
        {
          path: 'create', component: CreateLocationComponent
        }
        ]
      },
      {
        path: 'events', component: EventsComponent, children: [
          {
            path: 'create', component: CreateEventComponent
          }
        ]
      },
      {
        path: 'events/:id', component: ReadEventComponent
      },
      {
        path: 'zones', component: ZonesComponent
      }

    ]
  },
  {
    path: 'login', pathMatch: 'full', component: LoginComponent
  },
  // {path: '404', component}
  { path: '**', redirectTo: '404' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
