import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'https://your-backend-api.com/chat'; // Replace with actual API (https://3c5e-2405-201-c439-8008-e1a9-8c73-cbd1-b0cf.ngrok-free.app/generate-openai-ol)
  private jsonUrl = 'generated-tests.json'; 
  private getTestSuiteUrl = 'http://localhost:8001/features/'; 
  private getTestUrl = 'http://localhost:8001/features/'; 
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
    return this.http.get<any>(this.getTestUrl+_id); // ✅ Fetch JSON data
  }
}
