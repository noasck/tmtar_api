import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { RepositoryService } from 'src/app/shared/services/repository.service';
import { Location } from '../locations/location.service';
export interface Zone {
    id?: number,
    title?: string,
    latitude?: number,
    longitude?: number,
    radius?: number,
    location_id?: number,
    active?: boolean,
    secret?: boolean,


    draggable?: boolean
    location?: Location
}
@Injectable({
    providedIn: 'root',
})
export class ZonesService {
    route = 'zones/';
    constructor(public repository: RepositoryService) { }

    getZones(): Observable<Zone[]> {
        return this.repository.getData<Zone[]>(this.route);
    }

    updateZone(id: number, Zone: Zone): Observable<Zone> {
        return this.repository.update<Zone>(this.route + String(id), Zone);
    }

    deleteZoneByID(id: number): Observable<null> {
        return this.repository.delete<null>(this.route + String(id));
    }

    createZone(Zone: Zone): Observable<Zone> {
        return this.repository.create<Zone>(this.route, Zone);
    }
}
