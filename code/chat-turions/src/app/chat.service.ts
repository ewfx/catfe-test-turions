import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private baseURL =
    //'https://3b28-2405-201-c439-8008-6939-d64c-40c9-ab06.ngrok-free.app'; 
    'http://localhost:5000'
  // privateOpenAPI =
  //   'https://3b28-2405-201-c439-8008-6939-d64c-40c9-ab06.ngrok-free.app/generate-openai-ol';

  options = new HttpHeaders({
    accept: 'application/json',
    'Content-Type': 'application/json',
  });
  private apiUrl = this.baseURL + '/generate-openai-ol';
  private jsonUrl = 'generated-tests.json';
  // private getTestSuiteUrl = this.baseURL + '/features/'; //http://localhost:8001/features/'; //temp cooment
  // private getTestSuiteUrl = 'test-suite.json';
  private getTestSuiteUrl = 'http://localhost:5000/features';
  private getTestUrl = 'test.json';
  // private getTestUrl = this.baseURL + '/features'; //'http://localhost:8001/features/';
  private saveTestURL = this.baseURL + '/features/'; //'http://127.0.0.1:8001/features/';

  headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization: 'Bearer YOUR_TOKEN_HERE',
  });

  constructor(private http: HttpClient) {}

  sendMessage(requestBody: { context: string }) {
    // return this.http.post<{ response: string }>(this.apiUrl, { message }, {});
    const opt = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Accept: 'application/json',
      }),
    };
    return this.http.post(this.apiUrl, requestBody, opt);
  }

  getGeneratedTests(): Observable<any[]> {
    return this.http.get<any[]>(this.jsonUrl); // ✅ Fetch JSON data
  }

  getTestSuite(): Observable<any[]> {
    const opt = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
    };
    return this.http.get<any[]>(this.getTestSuiteUrl, opt); // ✅ Fetch JSON data
  }

  // getTest(_id: any): Observable<any> {
  //   return this.http.get<any>(this.getTestUrl + _id); // ✅ Fetch JSON data
  // }

  getTest(_id: any): Observable<any> {
    return this.http.get<any>(this.getTestUrl); // ✅ Fetch JSON data
  }

  getFeatureData(): Observable<any> {
    return this.http.get<any>(this.getTestUrl); // ✅ Fetch JSON data
  }

  saveTestFeatures(data: any) {
    const opt = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Accept: 'application/json',
      }),
    };
    return this.http.post(this.saveTestURL, data, opt);
  }
}
