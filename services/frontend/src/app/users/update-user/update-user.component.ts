import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { User, UserService } from '../user.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Location, LocationService } from 'src/app/locations/location.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-update-user',
  templateUrl: './update-user.component.html',
  styleUrls: ['./update-user.component.scss'],
})
export class UpdateUserComponent implements OnInit {
  public user: FormGroup;
  errorMessage: string;
  allUsers: User[];
  allLocations: Location[];

  src: string = '';

  filteredLocations: Observable<Location[]>;

  @Output() close = new EventEmitter<void>();
  @Output() update = new EventEmitter<void>();

  @Input() fetchedUser: User;

  constructor(
    private userService: UserService,
    private locationService: LocationService
  ) {}

  ngOnInit(): void {
    this.getLocations();

    this.user = new FormGroup({
      admin_location: new FormControl(null, [Validators.required]),
    });
  }

  updateUser(): void {
    let data = this.user.value;
    const changes = {
      admin_location_id: data.admin_location.id,
    };

    this.userService.updateUser(this.fetchedUser.id, changes).subscribe(
      (res) => {
        this.fetchedUser = res;

        //get name of user location
        this.fetchedUser.location = this.getLocationName(
          this.fetchedUser.location_id
        );
        this.fetchedUser.adminLocation = this.getLocationName(
          this.fetchedUser.admin_location_id
        );
        this.update.emit();
      },
      (err) => {
        this.errorMessage = String(err);
      },
      () => {
        this.errorMessage = null;
      }
    );
    this.user.reset();
    this.src = '';
    this.getLocations();
  }

  getLocations() {
    //for autocomplete
    this.locationService.getLocations().subscribe(
      (res) => {
        //get user location id
        let userLocationId = +localStorage.getItem('user_location_id');

        //get all children locations for user location
        this.allLocations = this.locationService.getLocationChildren(
          res,
          userLocationId
        );

        //set parent name for all location
        this.allLocations.map((l) => {
          if (l.id != 1) {
            this.locationService.getParentName(l);
          }
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
    );
  }

  getLocationName(id): string {
    let name = this.allLocations.filter((location) => location.id === id)[0]
      .name;
    return name;
  }

  displayFn(loc: Location): string {
    return loc && loc.name ? loc.name : '';
  }
}
