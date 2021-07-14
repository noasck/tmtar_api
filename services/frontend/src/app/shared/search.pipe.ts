import { Pipe, PipeTransform } from '@angular/core';
@Pipe({
  name: 'search'
})
export class SearchPipe implements PipeTransform {
  //search user by field
  transform(value: any, str: any, field: string = "id"): any {
    if(!str){
      return value
    }
    return value.filter((user) =>
      user[field].toString().toLowerCase().includes(str.toLowerCase()));
  }
}
