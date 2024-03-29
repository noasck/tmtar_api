import { HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { EnvironmentUrlService } from '../shared/services/environment-url.service';
import { RepositoryService } from '../shared/services/repository.service';

export interface FileResponse {
  id: number;
  filename: string;
  
  extention?: string;
}

@Injectable({
  providedIn: 'root'
})
export class FileService {
  ROUTE = 'files/';

  constructor(private repo: RepositoryService, private envUrl: EnvironmentUrlService) { }

  postFile(data): Observable<FileResponse> {
    return this.repo.create<FileResponse>(this.ROUTE, data);
  }

  getFiles(): Observable<FileResponse[]> {
    return this.repo.getData<FileResponse[]>(this.ROUTE);
  }

  deleteFile(filename): Observable<null> {
    return this.repo.delete<null>(this.ROUTE + filename)
  }

  getFileByName(filename): string {
    return this.envUrl.apiUrl + '/' + this.ROUTE + filename
  }
}