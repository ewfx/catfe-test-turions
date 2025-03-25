import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'https://your-backend-api.com/chat'; // Replace with actual API URL
  private jsonUrl = 'generated-tests.json'; 
  private getTestSuiteUrl = 'test-suite.json'; 
  private getTestUrl = 'test.json'; 
  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<{ response: string }> {
    return this.http.post<{ response: string }>(this.apiUrl, { message });
  }

  getGeneratedTests(): Observable<any[]> {
    return this.http.get<any[]>(this.jsonUrl); // ✅ Fetch JSON data
  }

  getTestSuite(): Observable<any[]> {
    return this.http.get<any[]>(this.getTestSuiteUrl); // ✅ Fetch JSON data
  }

  getTest(_id: any): Observable<any> {
    return this.http.get<any>(this.getTestUrl); // ✅ Fetch JSON data
  }
}
