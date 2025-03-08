"""
ISO/IEC/IEEE 29119標準に基づいたデフォルトのセクションテンプレート
"""

# テスト計画のデフォルトセクション
TEST_PLAN_SECTIONS = [
    {
        'title': 'テスト計画の識別',
        'description': 'テスト計画の識別情報',
        'form_type': 'text',
        'content_guidelines': 'テスト計画の一意の識別子、バージョン、日付を含めてください。',
        'ai_prompt': 'テスト計画の識別情報（ID、バージョン、日付など）を生成してください。',
        'order': 1
    },
    {
        'title': 'はじめに',
        'description': 'テスト計画の目的と範囲',
        'form_type': 'textarea',
        'content_guidelines': 'テスト計画の目的、テスト対象、テストの範囲を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト計画の目的と範囲を説明してください。',
        'order': 2
    },
    {
        'title': 'テスト項目',
        'description': 'テスト対象のコンポーネントや機能',
        'form_type': 'textarea',
        'content_guidelines': 'テスト対象となるソフトウェアコンポーネント、機能、特性を列挙してください。',
        'ai_prompt': '製品説明に基づいて、テスト対象となるコンポーネントや機能のリストを生成してください。',
        'order': 3
    },
    {
        'title': 'テスト特性',
        'description': 'テストする品質特性',
        'form_type': 'textarea',
        'content_guidelines': 'テストする品質特性（機能性、信頼性、使用性、効率性、保守性、移植性など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストすべき品質特性を特定し、それぞれについて説明してください。',
        'order': 4
    },
    {
        'title': 'テスト設計手法',
        'description': 'テストケース設計に使用する手法',
        'form_type': 'textarea',
        'content_guidelines': 'テストケース設計に使用する手法（同値分割、境界値分析、状態遷移テストなど）を説明してください。',
        'ai_prompt': '製品説明に基づいて、適切なテスト設計手法を提案し、それぞれの手法をどのように適用するかを説明してください。',
        'order': 5
    },
    {
        'title': 'テスト完了基準',
        'description': 'テスト完了を判断する基準',
        'form_type': 'textarea',
        'content_guidelines': 'テスト完了を判断する基準（テストカバレッジ、欠陥密度、重大な欠陥の不在など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、適切なテスト完了基準を定義してください。',
        'order': 6
    },
    {
        'title': 'テスト中断と再開の基準',
        'description': 'テストを中断および再開する条件',
        'form_type': 'textarea',
        'content_guidelines': 'テストを中断する条件と再開するための基準を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストを中断すべき状況と再開するための条件を定義してください。',
        'order': 7
    },
    {
        'title': 'テスト成果物',
        'description': 'テスト活動から生成される文書',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動から生成される文書（テスト計画、テスト仕様書、テスト結果報告書など）を列挙してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動から生成されるべき文書のリストを作成してください。',
        'order': 8
    },
    {
        'title': 'テスト環境',
        'description': 'テストに必要なハードウェアとソフトウェア',
        'form_type': 'textarea',
        'content_guidelines': 'テストに必要なハードウェア、ソフトウェア、ネットワーク環境を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストに必要な環境（ハードウェア、ソフトウェア、ネットワークなど）を詳細に説明してください。',
        'order': 9
    },
    {
        'title': '役割と責任',
        'description': 'テスト活動に関わる役割と責任',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動に関わる役割（テストマネージャー、テスト設計者、テスト実行者など）とその責任を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動に必要な役割とそれぞれの責任を定義してください。',
        'order': 10
    },
    {
        'title': 'スケジュール',
        'description': 'テスト活動のスケジュール',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動のスケジュール（テスト計画、テスト設計、テスト実行、テスト評価のマイルストーン）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動の詳細なスケジュールを作成してください。',
        'order': 11
    },
    {
        'title': 'リスクと対策',
        'description': 'テスト活動に関連するリスクと対策',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動に関連するリスクとその対策を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動に関連する潜在的なリスクを特定し、それぞれに対する対策を提案してください。',
        'order': 12
    },
    {
        'title': '承認',
        'description': 'テスト計画の承認',
        'form_type': 'textarea',
        'content_guidelines': 'テスト計画の承認者と承認日を記載してください。',
        'ai_prompt': 'テスト計画の承認に関する情報を生成してください。',
        'order': 13
    }
]

# テスト仕様書のデフォルトセクション
TEST_SPECIFICATION_SECTIONS = [
    {
        'title': 'テスト仕様書の識別',
        'description': 'テスト仕様書の識別情報',
        'form_type': 'text',
        'content_guidelines': 'テスト仕様書の一意の識別子、バージョン、日付を含めてください。',
        'ai_prompt': 'テスト仕様書の識別情報（ID、バージョン、日付など）を生成してください。',
        'order': 1
    },
    {
        'title': 'はじめに',
        'description': 'テスト仕様書の目的と範囲',
        'form_type': 'textarea',
        'content_guidelines': 'テスト仕様書の目的、テスト対象、テストの範囲を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト仕様書の目的と範囲を説明してください。',
        'order': 2
    },
    {
        'title': 'テスト項目',
        'description': 'テスト対象のコンポーネントや機能',
        'form_type': 'textarea',
        'content_guidelines': 'テスト対象となるソフトウェアコンポーネント、機能、特性を詳細に説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト対象となるコンポーネントや機能の詳細な説明を生成してください。',
        'order': 3
    },
    {
        'title': 'テスト条件',
        'description': 'テストする条件',
        'form_type': 'textarea',
        'content_guidelines': 'テストする条件（入力条件、環境条件、状態条件など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストすべき条件を特定し、それぞれについて説明してください。',
        'order': 4
    },
    {
        'title': 'テストケース',
        'description': 'テストケースの詳細',
        'form_type': 'textarea',
        'content_guidelines': 'テストケースの詳細（ID、目的、前提条件、手順、期待結果など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、詳細なテストケースを生成してください。各テストケースには、ID、目的、前提条件、手順、期待結果を含めてください。',
        'order': 5
    },
    {
        'title': 'テストデータ',
        'description': 'テストに必要なデータ',
        'form_type': 'textarea',
        'content_guidelines': 'テストに必要なデータ（入力データ、参照データ、出力データなど）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストに必要なデータの詳細を生成してください。',
        'order': 6
    },
    {
        'title': 'テスト環境',
        'description': 'テストに必要な環境',
        'form_type': 'textarea',
        'content_guidelines': 'テストに必要な環境（ハードウェア、ソフトウェア、ネットワーク、ツールなど）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストに必要な環境の詳細を生成してください。',
        'order': 7
    },
    {
        'title': 'テスト手順',
        'description': 'テスト実行の手順',
        'form_type': 'textarea',
        'content_guidelines': 'テスト実行の手順（セットアップ、実行、クリーンアップなど）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト実行の詳細な手順を生成してください。',
        'order': 8
    },
    {
        'title': '合格基準',
        'description': 'テストの合格基準',
        'form_type': 'textarea',
        'content_guidelines': 'テストの合格基準（期待結果との一致、パフォーマンス基準の達成など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テストの合格基準を定義してください。',
        'order': 9
    },
    {
        'title': '承認',
        'description': 'テスト仕様書の承認',
        'form_type': 'textarea',
        'content_guidelines': 'テスト仕様書の承認者と承認日を記載してください。',
        'ai_prompt': 'テスト仕様書の承認に関する情報を生成してください。',
        'order': 10
    }
]

# テスト結果報告書のデフォルトセクション
TEST_REPORT_SECTIONS = [
    {
        'title': 'テスト結果報告書の識別',
        'description': 'テスト結果報告書の識別情報',
        'form_type': 'text',
        'content_guidelines': 'テスト結果報告書の一意の識別子、バージョン、日付を含めてください。',
        'ai_prompt': 'テスト結果報告書の識別情報（ID、バージョン、日付など）を生成してください。',
        'order': 1
    },
    {
        'title': 'はじめに',
        'description': 'テスト結果報告書の目的と範囲',
        'form_type': 'textarea',
        'content_guidelines': 'テスト結果報告書の目的、テスト対象、テストの範囲を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト結果報告書の目的と範囲を説明してください。',
        'order': 2
    },
    {
        'title': 'テスト概要',
        'description': 'テスト活動の概要',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動の概要（テスト期間、テスト環境、テスト実行者など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動の概要を生成してください。',
        'order': 3
    },
    {
        'title': 'テスト結果',
        'description': 'テスト結果の詳細',
        'form_type': 'textarea',
        'content_guidelines': 'テスト結果の詳細（合格したテスト、失敗したテスト、未実行のテストなど）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト結果の詳細を生成してください。',
        'order': 4
    },
    {
        'title': '欠陥概要',
        'description': '発見された欠陥の概要',
        'form_type': 'textarea',
        'content_guidelines': '発見された欠陥の概要（欠陥の数、重要度、優先度など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、発見された欠陥の概要を生成してください。',
        'order': 5
    },
    {
        'title': '欠陥詳細',
        'description': '発見された欠陥の詳細',
        'form_type': 'textarea',
        'content_guidelines': '発見された欠陥の詳細（ID、説明、再現手順、影響、重要度、優先度など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、発見された欠陥の詳細を生成してください。',
        'order': 6
    },
    {
        'title': 'テスト評価',
        'description': 'テスト活動の評価',
        'form_type': 'textarea',
        'content_guidelines': 'テスト活動の評価（テスト完了基準の達成状況、テストカバレッジ、テスト効率など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト活動の評価を生成してください。',
        'order': 7
    },
    {
        'title': '結論と推奨事項',
        'description': 'テスト結果に基づく結論と推奨事項',
        'form_type': 'textarea',
        'content_guidelines': 'テスト結果に基づく結論と推奨事項（リリース可否、追加テストの必要性、リスク軽減策など）を説明してください。',
        'ai_prompt': '製品説明に基づいて、テスト結果に基づく結論と推奨事項を生成してください。',
        'order': 8
    },
    {
        'title': '承認',
        'description': 'テスト結果報告書の承認',
        'form_type': 'textarea',
        'content_guidelines': 'テスト結果報告書の承認者と承認日を記載してください。',
        'ai_prompt': 'テスト結果報告書の承認に関する情報を生成してください。',
        'order': 9
    }
]

# テスト文書タイプとそのデフォルトセクションのマッピング
DEFAULT_TEMPLATES = {
    'test_plan': {
        'name': 'テスト計画書',
        'description': 'ISO/IEC/IEEE 29119に準拠したテスト計画書',
        'sections': TEST_PLAN_SECTIONS
    },
    'test_specification': {
        'name': 'テスト仕様書',
        'description': 'ISO/IEC/IEEE 29119に準拠したテスト仕様書',
        'sections': TEST_SPECIFICATION_SECTIONS
    },
    'test_report': {
        'name': 'テスト結果報告書',
        'description': 'ISO/IEC/IEEE 29119に準拠したテスト結果報告書',
        'sections': TEST_REPORT_SECTIONS
    }
} 