import { Component, OnInit } from '@angular/core';
import { LocationService } from 'src/app/locations/location.service';
import { User, UserService } from '../user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {
  fetchedUsers: User[];
  fetched: boolean;
  errorMessage: string;
  indicator: boolean = false;
  keys: string[];
  deleteU: number | string
  //usersLocations: UserLoc[] = [];
  //userShown: boolean;

  searchField: string = "id"
  src: string = ""

  userChange: User
  
  constructor(private userService: UserService, private locationService: LocationService) {
   }

  ngOnInit(): void {
    //get all users on component initialization
    this.getAllUsers()
    
  }

  getAllUsers(){
    this.fetched = false;
    this.userService.getUsers().subscribe(
      (res) => {
        this.fetchedUsers = res;

        //this.keys = Object.keys(this.fetchedUsers[0])

        // get locations objects for users
        this.fetchedUsers.map((user) => {
          this.getLocation(user, user.location_id, user.admin_location_id)
        })

      },
      (error) => {
        this.errorMessage = error;
      },
      () => {
        this.fetched = true;
      }
    );
  }

  getLocation(user, lid, alid): void{
    //get user`s adminLocation and location as object
    this.locationService.getLocationsByID(lid).subscribe(
      (res) => {
        user.location = res
      },
      (error) => {
        this.errorMessage = String(error);
      }, () => {
        this.errorMessage = null;
      }
    )

    this.locationService.getLocationsByID(alid).subscribe(
      (res) => {
        user.adminLocation = res
      },
      (error) => {
        this.errorMessage = String(error);
      }, () => {
        this.errorMessage = null;
      }
    )
  }

  deleteUser(delOption, id): void{
    //removes user with specified id
    if(delOption){
      this.userService.deleteUserByID(id).subscribe(
        () => { this.fetchedUsers = this.fetchedUsers.filter(user => user.id!=id) }
      );
    }
    this.deleteU = null
  }

  multipleDelete(delOption): void{
   let users = this.getCheckedCheckBoxes();
    for(let id of users){
      this.deleteUser(delOption, id);
    }
  }

  getCheckedCheckBoxes(){
    let selectedCheckBoxes = document.querySelectorAll('input.checkbox:checked') ;
    let  checkedValues = Array.from(selectedCheckBoxes).map(userCheck => (userCheck as HTMLInputElement).value);
    return checkedValues
  }

  byField(field){
    if(this.indicator){
      return (a, b) => a[field] > b[field] ? -1 : 1;
    }
    else{
      return (a, b) => a[field] > b[field] ? 1 : -1;
    }
  }
  
  sort(field){
    this.indicator = !this.indicator
    this.fetchedUsers.sort(this.byField(field))
  }
 
}
