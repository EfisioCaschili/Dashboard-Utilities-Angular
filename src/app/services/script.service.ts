import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ScriptService {
  constructor(private api: ApiService, private http: HttpClient) {}

  runScript(script: string, params: any): Observable<any> {
    console.log('Running script:', script, 'with params:', params);
    return this.api.post('run_script', { script, params });
  }
}
