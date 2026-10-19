import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// Emulator: 10.0.2.2 | Real phone: your laptop IP, e.g. 192.168.1.5
const String apiBase = 'http://127.0.0.1:8000';

void main() => runApp(const ScamShieldApp());

class ScamShieldApp extends StatelessWidget {
  const ScamShieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tanglish Scam Shield',
      theme: ThemeData(
        colorSchemeSeed: Colors.indigo,
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _controller = TextEditingController();
  Map<String, dynamic>? _result;
  bool _loading = false;
  bool _tamil = false;
  String? _error;

  Future<void> _check() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _loading = true;
      _error = null;
      _result = null;
    });

    try {
      final res = await http
          .post(
            Uri.parse('$apiBase/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'text': text}),
          )
          .timeout(const Duration(seconds: 10));

      if (res.statusCode == 200) {
        setState(() => _result = jsonDecode(utf8.decode(res.bodyBytes)));
      } else {
        setState(() => _error = 'Server error: ${res.statusCode}');
      }
    } catch (e) {
      setState(() => _error = 'Server ku connect aagala. API run aagudha paarunga.');
    } finally {
      setState(() => _loading = false);
    }
  }

  Color _color(String label) {
    switch (label) {
      case 'scam':
        return Colors.red;
      case 'suspicious':
        return Colors.orange;
      default:
        return Colors.green;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tanglish Scam Shield'),
        actions: [
          TextButton(
            onPressed: () => setState(() => _tamil = !_tamil),
            child: Text(_tamil ? 'Tanglish' : 'தமிழ்'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _controller,
              maxLines: 5,
              decoration: const InputDecoration(
                hintText: 'Sandhegam irukkura message ah inga paste pannunga',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: _loading ? null : _check,
              child: _loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Check pannunga'),
            ),
            const SizedBox(height: 16),
            if (_error != null)
              Text(_error!, style: const TextStyle(color: Colors.red)),
            if (_result != null) _buildResult(_result!),
          ],
        ),
      ),
    );
  }

  Widget _buildResult(Map<String, dynamic> r) {
    final label = r['label'] as String;
    final conf = ((r['confidence'] as num) * 100).round();
    final reasons = List<String>.from(
        _tamil ? r['reasons_tamil'] : r['reasons_tanglish']);
    final advice = _tamil ? r['advice_tamil'] : r['advice_tanglish'];
    final color = _color(label);

    return Card(
      color: color.withValues(alpha: 0.1),
      shape: RoundedRectangleBorder(
        side: BorderSide(color: color, width: 1.5),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${label.toUpperCase()}  ($conf%)',
              style: TextStyle(
                  fontSize: 22, fontWeight: FontWeight.bold, color: color),
            ),
            if (reasons.isNotEmpty) ...[
              const SizedBox(height: 12),
              Text(_tamil ? 'ஏன்?' : 'Yen?',
                  style: const TextStyle(fontWeight: FontWeight.bold)),
              for (final reason in reasons) Text('• $reason'),
            ],
            const SizedBox(height: 12),
            Text(advice),
          ],
        ),
      ),
    );
  }
}