import { Component, OnInit } from '@angular/core';
import { User, UserService } from '../user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
})
export class UserComponent implements OnInit {
  fetchedUsers: User[];
  fetched: boolean;
  errorMessage: string;
  indicator: boolean = false;
  keys: string[];
  deleteU: number | string;

  searchField: string = 'id';
  src: string = '';

  userChange: User;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    //get all users on component initialization
    this.getAllUsers();
  }

  getAllUsers() {
    this.fetched = false;
    this.userService.getUsers().subscribe(
      (res) => {
        this.fetchedUsers = res;

        //this.keys = Object.keys(this.fetchedUsers[0])

        // get locations objects for users
        this.fetchedUsers.map((user) => {
          //this.getLocation(user, user.location_id, user.admin_location_id);
          this.userService.getUserLocationName(user.location_id, 'Loc', user);
          this.userService.getUserLocationName(
            user.admin_location_id,
            'adminLoc',
            user
          );
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {
        this.fetched = true;
      }
    );
  }

  deleteUser(delOption, id): void {
    //removes user with specified id
    if (delOption) {
      this.userService.deleteUserByID(id).subscribe(() => {
        this.fetchedUsers = this.fetchedUsers.filter((user) => user.id != id);
      });
    }
    this.deleteU = null;
  }

  multipleDelete(delOption): void {
    //if user picked deletion with checkboxes
    let users = this.getCheckedCheckBoxes();
    for (let id of users) {
      this.deleteUser(delOption, id);
    }
  }

  getCheckedCheckBoxes() {
    let selectedCheckBoxes = document.querySelectorAll(
      'input.checkbox:checked'
    );
    let checkedValues = Array.from(selectedCheckBoxes).map(
      (userCheck) => (userCheck as HTMLInputElement).value
    );
    return checkedValues;
  }

  sort(field) {
    this.indicator = !this.indicator;
    this.fetchedUsers.sort(this.byField(field));
  }

  byField(field) {
    if (this.indicator) {
      return (a, b) => (a[field] > b[field] ? -1 : 1);
    } else {
      return (a, b) => (a[field] > b[field] ? 1 : -1);
    }
  }
}
