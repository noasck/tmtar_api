import { Pipe, PipeTransform } from '@angular/core';
import { Location } from 'src/app/locations/location.service';

@Pipe({ name: 'startsWith' })
export class AutocompletePipe implements PipeTransform {
  public transform(locations: Location[], str = '') {
    if (!str) {
      return locations;
    }
    return locations.filter((l) =>
      l.name.toString().toLowerCase().startsWith(str.toString().toLowerCase())
    );
  }
}
