import { Component, OnInit, output } from '@angular/core';
import { HttpClient, HttpHeaders  } from '@angular/common/http';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent   {

  output: any = null;

  constructor(private http: HttpClient) {}
  
  ngOnInit(): void {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {}
    this.http.post('http://127.0.0.1:5000/api/sim_dashboard/status', body, { headers })
      .subscribe({
        next: (response) => {
          this.output = response;
          console.log('Home data:', this.output);
        },
        error: (err) => {
          console.error('Errore caricamento dati Home:', err);
        }
      });
}

}
