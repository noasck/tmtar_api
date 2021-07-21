import { Injectable, OnInit } from '@angular/core';
import { RepositoryService } from '../shared/services/repository.service';
import { Observable } from 'rxjs';
import { Location, LocationService } from '../locations/location.service';
export interface User {
  id: number;
  location_id?: number;
  bdate?: Date;
  email_hash?: string;
  admin_location_id?: number;
  sex?: string;

  //location?: Location;
  //adminLocation?: Location;
  location: string;
  adminLocation: string;
}

export interface CurrentUser {
  location_id?: number;
  sex?: string;
  identity?: string;
  bdate?: string;
  id?: number;
  admin_location_id?: number;
}

@Injectable({
  providedIn: 'root',
})
export class UserService {
  route = 'users/';
  constructor(
    public repository: RepositoryService,
    private locationService: LocationService
  ) {}

  updateCurrentUser(data): Observable<CurrentUser> {
    return this.repository.update<CurrentUser>(this.route, data);
  }

  getUsers(): Observable<User[]> {
    return this.repository.getData<User[]>(this.route);
  }

  getUserByID(id: number): Observable<User> {
    return this.repository.getData<User>(this.route + String(id));
  }

  updateUser(id: number, user): Observable<User> {
    return this.repository.update<User>(this.route + String(id), user);
  }

  deleteUserByID(id: number): Observable<null> {
    return this.repository.delete<null>(this.route + String(id));
  }

  /* createUser(user: User): Observable<User> {
     return this.repository.create<User>(this.route + String(user.id), user);
   }*/

  getUserLocationName(id, option, user) {
    /* id - user`s location id
      option - what location name we want to get
    */
    this.locationService.getLocationsByID(id).subscribe(
      (res) => {
        if (option == 'Loc') {
          user.location = res.name;
        } else if (option == 'adminLoc') {
          user.adminLocation = res.name;
        }
      },
      (error) => {
        console.log(error);
      }
    );
  }
}
