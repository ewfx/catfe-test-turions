import { Component, Input, OnInit, inject } from '@angular/core';
import { ChatService } from '../app/chat.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-test-suite',
  imports: [CommonModule, FormsModule],
  templateUrl: './test-suite.component.html',
  styleUrl: './test-suite.component.css'
})
export class TestSuiteComponent implements OnInit{
  @Input() id: string = '';
  testContext = ''; // User input context
  generatedTests: any; // Stores generated test scenarios
  constructor(private route: ActivatedRoute) {}
  private testService = inject(ChatService); // Inject Service

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id') || '';
    this.testService.getTest(this.id).subscribe((tests) => {
      this.generatedTests = tests; // ✅ Load test cases from JSON
    });
  }
  generateTests() {
    this.testService.getGeneratedTests().subscribe((tests) => {
      this.generatedTests = tests; // ✅ Load test cases from JSON
    });
  }
}
