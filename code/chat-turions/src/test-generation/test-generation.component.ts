import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../app/chat.service';

@Component({
  selector: 'app-test-generation',
  standalone: true, 
  imports: [CommonModule, FormsModule],
  templateUrl: './test-generation.component.html',
  styleUrl: './test-generation.component.css'
})
export class TestGenerationComponent {
  testContext = ''; // User input context
  generatedTests: any[] = []; // Stores generated test scenarios

  private testService = inject(ChatService); // Inject Service

  generateTests() {
    this.testService.getGeneratedTests().subscribe((tests) => {
      this.generatedTests = tests; // ✅ Load test cases from JSON
    });
  }
}
