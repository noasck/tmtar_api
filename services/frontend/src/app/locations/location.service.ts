import { ComponentFactoryResolver, Injectable, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { RepositoryService } from 'src/app/shared/services/repository.service';
export interface Location {
  name?: string;
  id?: number;
  root?: number;

  parentName?: string;
}
@Injectable({
  providedIn: 'root',
})
export class LocationService {
  route = 'locations/';
  constructor(public repository: RepositoryService) {}

  getLocations(): Observable<Location[]> {
    return this.repository.getData<Location[]>(this.route);
  }

  getLocationsByID(id: number): Observable<Location> {
    return this.repository.getData<Location>(this.route + String(id));
  }

  getParent(id: number): Observable<Location> {
    return this.repository.getData<Location>(
      this.route + 'parent/' + String(id)
    );
  }

  updateLocation(id: number, location: Location): Observable<Location> {
    return this.repository.update<Location>(this.route + String(id), location);
  }

  search(str: string) {
    return this.repository.getData<Location[]>(this.route + 'search/' + str);
  }

  deleteLocationByID(id: number): Observable<null> {
    return this.repository.delete<null>(this.route + String(id));
  }

  createLocation(location: Location): Observable<Location> {
    return this.repository.create<Location>(this.route, location);
  }

  getParentName(location) {
    this.getParent(location.id).subscribe(
      (res) => {
        location.parentName = res.name;
      },
      (error) => {
        //this.errorMessage = String(error);
      },
      () => {
        //this.errorMessage = null;
      }
    );
  }

  getLocationChildren(locations, id): Location[] {
    let children: Location[] = [];
    this.getChildren(locations, id, children);
    return children;
  }

  private getChildren(locations, id, children) {
    locations.map((l) => {
      if (l.id == id) {
        children.push(l);
      } else if (l.root == id) {
        this.getChildren(locations, l.id, children);
      }
    });
    return;
  }

   getLocationName(id) {
    let location: Location
    this.getLocationsByID(id).subscribe(
        (res) => {
          location = res
          console.log("hello")  
        },
        (error) => {
          console.log(error);
        }
      )

    console.log("location", location)
    return location.name;
  }

  getAdminLocationName(id): string {
    let name: string;
    this.getParent(id).subscribe(
      (res) => {
        name = res.name;
      },
      (error) => {
        console.log(error);
      }
    );

    return name;
  }
}
